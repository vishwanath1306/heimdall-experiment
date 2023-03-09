import heimdall_jaeger_parse

val3 = heimdall_jaeger_parse.JRoot(filename="../jaeger_traces.json")
print(val3.data[0].trace_id)
for span in val3.data[0].spans:
    if len(span.references) != 0:
        print(span.span_id, span.references[0].ref_type, span.references[0].span_id)


# /Users/vishwanath/Developer/Rust/trace-graph-store/base_storage/example_personal/example_personal_string.json