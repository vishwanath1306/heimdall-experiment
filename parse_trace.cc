/*

Program to read the output of hindsight traces. Partly adpated from the process.cc in microbricks. 

*/

#include <iostream>
#include <string>
#include <iomanip>
#include <argp.h>
#include <fstream>
#include <sstream>

extern "C" {
    #include "tracer/tracestate.h"
}

// ============ START ARGUMENTS ===================

static char doc[] = "For parsing the hindsight collector output";
static char args_doc[] = "FILENAME";

bool DEBUG = false;
bool WARN = false; 

static struct argp_option options [] = {
    {"debug", 'd', 0, 0, "Print debug information"},
    {"warn", 'w', 0, 0, "Print warnings"},
    { 0 }
};

struct arguments {
    bool debug;
    bool warn;
    std::string ip_file;
    std::string op_file;
};

static error_t parse_opt(int key, char *arg, struct argp_state *state){
    struct arguments *args = (struct arguments*) state->input;

    switch (key)
    {
    case 'd':
        args->debug = true;
        break;
    case 'w': 
        args->warn = true;
        break;
    case ARGP_KEY_ARG:
        if(state->arg_num >= 1)
        argp_usage(state);
        args->ip_file = std::string(arg);
        break;
    case ARGP_KEY_END:
        if (state->arg_num <1)
        argp_usage(state);
        break;
    default:
        return ARGP_ERR_UNKNOWN;
    }
    return 0;
}

static struct argp argp = {options, parse_opt, args_doc, doc};

// ============ END ARGUMENTS ===================

// ============ START BUFFERS ===================

class RawHindsightBuffer {
    public: 
        std::string agent; 
        TraceHeader* header;

};

void read_buffers(std::string filename){
    std::fstream dataset_fd(filename, std::ios_base::in);

    dataset_fd.seekg(0, std::ios::end);
    size_t length = dataset_fd.tellg();
    dataset_fd.seekg(0, std::ios::beg);

    if(DEBUG){
        std::cout << filename << " has length " << length << std::endl;
    }


}

int main(int argc, char**argv){

    struct arguments args;
    args.debug = false;
    args.warn = false;

    argp_parse(&argp, argc, argv, 0, 0, &args);

    DEBUG = args.debug;
    WARN = args.warn;

    std::cout<<"input file is: "<<args.ip_file<<std::endl;

    read_buffers(args.ip_file);
    return 1;
}