#include <stdio.h>
#include "tracer/hindsight.h"
#include "tracer/agentapi.h"

#include "tracepoint.pb-c.h"

#define TRACEPOINT_TEXT_SIZE 1024

int main(){

    Tracepoint tracepoint = TRACEPOINT__INIT;
    char tracepoint_text[TRACEPOINT_TEXT_SIZE];
    hindsight_init("default");
    uint64_t trace_id = rand_uint64();
    hindsight_begin(trace_id);
    for (int i = 0; i < 100; i++) {
            tracepoint.service_name = "random_service";
            snprintf(tracepoint_text, sizeof(tracepoint_text), "Tracepoint value: %d", i+1);
            tracepoint.tracepoint_text = tracepoint_text;
            hindsight_tracepoint(tracepoint.tracepoint_text, sizeof(tracepoint.tracepoint_text));
    }
    hindsight_end();
}