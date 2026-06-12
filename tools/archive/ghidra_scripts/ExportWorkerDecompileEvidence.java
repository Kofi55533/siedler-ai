// Exports Ghidra decompiler evidence for worker/camp/path functions.
//
// Args:
//   0: worker_camp_path_branch_matrix.json
//   1: output json path
//   2: output markdown path

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileOptions;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.decompiler.DecompiledFunction;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Listing;
import ghidra.program.model.pcode.HighFunction;
import ghidra.program.model.pcode.PcodeOpAST;
import ghidra.program.model.symbol.Reference;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ExportWorkerDecompileEvidence extends GhidraScript {

    private static String jsonEscape(String s) {
        if (s == null) {
            return "";
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '\\': sb.append("\\\\"); break;
                case '"': sb.append("\\\""); break;
                case '\n': sb.append("\\n"); break;
                case '\r': sb.append("\\r"); break;
                case '\t': sb.append("\\t"); break;
                default:
                    if (c < 0x20) {
                        sb.append(String.format("\\u%04x", (int)c));
                    } else {
                        sb.append(c);
                    }
            }
        }
        return sb.toString();
    }

    private static String sha256(String text) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] digest = md.digest(text.getBytes(StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        for (byte b : digest) {
            sb.append(String.format("%02x", b & 0xff));
        }
        return sb.toString();
    }

    private static int lineCount(String text) {
        if (text == null || text.isEmpty()) {
            return 0;
        }
        int lines = 1;
        for (int i = 0; i < text.length(); i++) {
            if (text.charAt(i) == '\n') {
                lines++;
            }
        }
        return lines;
    }

    private static Set<String> loadTargetAddresses(File branchJson) throws Exception {
        String text = Files.readString(branchJson.toPath(), StandardCharsets.UTF_8);
        Pattern p = Pattern.compile("\"function\"\\s*:\\s*\"(0x[0-9a-fA-F]+)\"");
        Matcher m = p.matcher(text);
        Set<String> out = new LinkedHashSet<>();
        while (m.find()) {
            String raw = m.group(1).toLowerCase();
            long value = Long.decode(raw);
            out.add(String.format("0x%08x", value));
        }
        return out;
    }

    private String addressKey(Address address) {
        return String.format("0x%08x", address.getOffset());
    }

    private Map<String, Integer> pcodeHistogram(HighFunction hf) {
        Map<String, Integer> hist = new TreeMap<>();
        if (hf == null) {
            return hist;
        }
        Iterator<PcodeOpAST> it = hf.getPcodeOps();
        while (it.hasNext()) {
            PcodeOpAST op = it.next();
            String mnemonic = op.getMnemonic();
            hist.put(mnemonic, hist.getOrDefault(mnemonic, 0) + 1);
        }
        return hist;
    }

    private List<String> collectStringRefs(Function function, int limit) {
        List<String> refs = new ArrayList<>();
        Listing listing = currentProgram.getListing();
        for (Address addr : function.getBody().getAddresses(true)) {
            Reference[] refsFrom = currentProgram.getReferenceManager().getReferencesFrom(addr);
            for (Reference ref : refsFrom) {
                Address to = ref.getToAddress();
                if (to == null || !to.isMemoryAddress()) {
                    continue;
                }
                try {
                    ghidra.program.model.listing.Data data = listing.getDataAt(to);
                    if (data == null || !data.hasStringValue()) {
                        continue;
                    }
                    Object value = data.getValue();
                    if (value == null) {
                        continue;
                    }
                    String text = value.toString();
                    if (text.length() > 160) {
                        text = text.substring(0, 160);
                    }
                    String entry = addressKey(to) + ":" + text;
                    if (!refs.contains(entry)) {
                        refs.add(entry);
                    }
                    if (refs.size() >= limit) {
                        return refs;
                    }
                } catch (Exception ignored) {
                    // Some referenced data cannot be materialized as a string.
                }
            }
        }
        return refs;
    }

    private String histogramJson(Map<String, Integer> hist) {
        StringBuilder sb = new StringBuilder();
        sb.append("{");
        boolean first = true;
        for (Map.Entry<String, Integer> e : hist.entrySet()) {
            if (!first) {
                sb.append(",");
            }
            first = false;
            sb.append("\"").append(jsonEscape(e.getKey())).append("\":").append(e.getValue());
        }
        sb.append("}");
        return sb.toString();
    }

    private String stringListJson(List<String> values) {
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for (int i = 0; i < values.size(); i++) {
            if (i > 0) {
                sb.append(",");
            }
            sb.append("\"").append(jsonEscape(values.get(i))).append("\"");
        }
        sb.append("]");
        return sb.toString();
    }

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 3) {
            throw new IllegalArgumentException(
                "Expected args: <branch-matrix.json> <output.json> <output.md>"
            );
        }

        File branchJson = new File(args[0]);
        File outJson = new File(args[1]);
        File outMd = new File(args[2]);
        Set<String> targets = loadTargetAddresses(branchJson);

        DecompInterface decomp = new DecompInterface();
        DecompileOptions options = new DecompileOptions();
        decomp.setOptions(options);
        decomp.toggleCCode(true);
        decomp.toggleSyntaxTree(true);
        if (!decomp.openProgram(currentProgram)) {
            throw new IllegalStateException("Could not open program in decompiler");
        }

        List<String> jsonFunctions = new ArrayList<>();
        List<String> mdLines = new ArrayList<>();
        mdLines.add("# Ghidra Worker Decompile Evidence");
        mdLines.add("");
        mdLines.add("- Program: `" + currentProgram.getName() + "`");
        mdLines.add("- Executable path: `" + currentProgram.getExecutablePath() + "`");
        mdLines.add("- Language: `" + currentProgram.getLanguageID().getIdAsString() + "`");
        mdLines.add("- Compiler spec: `" + currentProgram.getCompilerSpec().getCompilerSpecID().getIdAsString() + "`");
        mdLines.add("- Generated: `" + Instant.now().toString() + "`");
        mdLines.add("- Target addresses from branch matrix: `" + targets.size() + "`");
        mdLines.add("");
        mdLines.add("This file stores decompiler metadata, P-Code histograms and SHA256 hashes of the generated C output. It intentionally does not inline full decompiled proprietary code.");
        mdLines.add("");
        mdLines.add("## Functions");
        mdLines.add("");

        Map<Function, List<String>> functionTargets = new LinkedHashMap<>();
        List<String> unmatchedTargets = new ArrayList<>();
        for (String target : targets) {
            Address targetAddress = toAddr(target);
            Function function = currentProgram.getFunctionManager().getFunctionAt(targetAddress);
            if (function == null) {
                function = currentProgram.getFunctionManager().getFunctionContaining(targetAddress);
            }
            if (function == null) {
                unmatchedTargets.add(target);
                continue;
            }
            List<String> mapped = functionTargets.get(function);
            if (mapped == null) {
                mapped = new ArrayList<>();
                functionTargets.put(function, mapped);
            }
            mapped.add(target);
        }

        int matchedTargets = targets.size() - unmatchedTargets.size();
        int decompiledOk = 0;
        for (Map.Entry<Function, List<String>> mappedFunction : functionTargets.entrySet()) {
            Function function = mappedFunction.getKey();
            List<String> targetAddresses = mappedFunction.getValue();
            String key = addressKey(function.getEntryPoint());
            boolean entryMatch = targetAddresses.contains(key);
            monitor.setMessage("Decompiling " + key + " " + function.getName());

            DecompileResults result = decomp.decompileFunction(function, 90, monitor);
            boolean ok = result != null && result.decompileCompleted();
            String error = ok ? "" : (result == null ? "no result" : result.getErrorMessage());
            String c = "";
            String cHash = "";
            int cLines = 0;
            Map<String, Integer> hist = new TreeMap<>();
            int pcodeOps = 0;
            if (ok) {
                DecompiledFunction df = result.getDecompiledFunction();
                if (df != null) {
                    c = df.getC();
                    cHash = sha256(c);
                    cLines = lineCount(c);
                }
                HighFunction hf = result.getHighFunction();
                hist = pcodeHistogram(hf);
                for (Integer count : hist.values()) {
                    pcodeOps += count;
                }
                decompiledOk++;
            }

            List<String> stringRefs = collectStringRefs(function, 24);
            long bodyAddresses = function.getBody().getNumAddresses();
            String signature = function.getSignature().toString();

            StringBuilder item = new StringBuilder();
            item.append("{");
            item.append("\"target_addresses\":").append(stringListJson(targetAddresses)).append(",");
            item.append("\"match_mode\":\"").append(entryMatch ? "entry" : "containing").append("\",");
            item.append("\"entry\":\"").append(key).append("\",");
            item.append("\"name\":\"").append(jsonEscape(function.getName())).append("\",");
            item.append("\"signature\":\"").append(jsonEscape(signature)).append("\",");
            item.append("\"body_address_count\":").append(bodyAddresses).append(",");
            item.append("\"decompile_completed\":").append(ok ? "true" : "false").append(",");
            item.append("\"decompile_error\":\"").append(jsonEscape(error)).append("\",");
            item.append("\"decompiled_c_sha256\":\"").append(cHash).append("\",");
            item.append("\"decompiled_c_line_count\":").append(cLines).append(",");
            item.append("\"pcode_op_count\":").append(pcodeOps).append(",");
            item.append("\"pcode_op_histogram\":").append(histogramJson(hist)).append(",");
            item.append("\"string_refs\":").append(stringListJson(stringRefs));
            item.append("}");
            jsonFunctions.add(item.toString());

            mdLines.add("### " + key + " `" + function.getName() + "`");
            mdLines.add("- target_addresses: `" + String.join(", ", targetAddresses) + "`");
            mdLines.add("- match_mode: `" + (entryMatch ? "entry" : "containing") + "`");
            mdLines.add("- signature: `" + signature.replace("`", "'") + "`");
            mdLines.add("- body_address_count: `" + bodyAddresses + "`");
            mdLines.add("- decompile_completed: `" + ok + "`");
            if (!ok) {
                mdLines.add("- decompile_error: `" + error.replace("`", "'") + "`");
            }
            mdLines.add("- decompiled_c_sha256: `" + cHash + "`");
            mdLines.add("- decompiled_c_line_count: `" + cLines + "`");
            mdLines.add("- pcode_op_count: `" + pcodeOps + "`");
            if (!hist.isEmpty()) {
                mdLines.add("- pcode_top_ops:");
                List<Map.Entry<String, Integer>> entries = new ArrayList<>(hist.entrySet());
                Collections.sort(entries, (a, b) -> b.getValue().compareTo(a.getValue()));
                int n = Math.min(12, entries.size());
                for (int i = 0; i < n; i++) {
                    Map.Entry<String, Integer> e = entries.get(i);
                    mdLines.add("  - `" + e.getKey() + "`: " + e.getValue());
                }
            }
            if (!stringRefs.isEmpty()) {
                mdLines.add("- referenced_strings:");
                for (String ref : stringRefs) {
                    mdLines.add("  - `" + ref.replace("`", "'") + "`");
                }
            }
            mdLines.add("");
        }

        StringBuilder json = new StringBuilder();
        json.append("{\n");
        json.append("  \"meta\": {\n");
        json.append("    \"generated_at_utc\": \"").append(Instant.now().toString()).append("\",\n");
        json.append("    \"tool\": \"Ghidra ").append(jsonEscape(getClass().getSimpleName())).append("\",\n");
        json.append("    \"program_name\": \"").append(jsonEscape(currentProgram.getName())).append("\",\n");
        json.append("    \"executable_path\": \"").append(jsonEscape(currentProgram.getExecutablePath())).append("\",\n");
        json.append("    \"language_id\": \"").append(jsonEscape(currentProgram.getLanguageID().getIdAsString())).append("\",\n");
        json.append("    \"compiler_spec_id\": \"").append(jsonEscape(currentProgram.getCompilerSpec().getCompilerSpecID().getIdAsString())).append("\",\n");
        json.append("    \"target_address_count\": ").append(targets.size()).append(",\n");
        json.append("    \"matched_target_address_count\": ").append(matchedTargets).append(",\n");
        json.append("    \"unmatched_target_address_count\": ").append(unmatchedTargets.size()).append(",\n");
        json.append("    \"matched_function_count\": ").append(functionTargets.size()).append(",\n");
        json.append("    \"decompiled_ok_count\": ").append(decompiledOk).append(",\n");
        json.append("    \"stores_full_decompiled_code\": false,\n");
        json.append("    \"unmatched_target_addresses\": ").append(stringListJson(unmatchedTargets)).append("\n");
        json.append("  },\n");
        json.append("  \"functions\": [\n");
        for (int i = 0; i < jsonFunctions.size(); i++) {
            if (i > 0) {
                json.append(",\n");
            }
            json.append("    ").append(jsonFunctions.get(i));
        }
        json.append("\n  ]\n");
        json.append("}\n");

        outJson.getParentFile().mkdirs();
        Files.writeString(outJson.toPath(), json.toString(), StandardCharsets.UTF_8);
        outMd.getParentFile().mkdirs();
        Files.write(outMd.toPath(), mdLines, StandardCharsets.UTF_8);

        println("Ghidra worker decompile evidence exported");
        println("Target addresses: " + targets.size());
        println("Matched target addresses: " + matchedTargets);
        println("Matched functions: " + functionTargets.size());
        println("Decompiled OK: " + decompiledOk);
        println("JSON: " + outJson.getAbsolutePath());
        println("MD: " + outMd.getAbsolutePath());
    }
}
