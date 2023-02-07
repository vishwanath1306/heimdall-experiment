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
        char* buf; 
        size_t size; 
        RawHindsightBuffer* next; 
        RawHindsightBuffer* prev;

        RawHindsightBuffer(std::string &agent, char* buf, size_t size)
        : agent(agent), buf(buf), next(nullptr), prev(nullptr), header((TraceHeader*) buf){}

        ~RawHindsightBuffer() {
            if(buf != nullptr){
                free(buf);
            }
        }

        std::string str(){
            std::stringstream s;
            s << "Buffer[";
            s << "Agent=" << agent;
            s << ", TraceID=" << header->trace_id;
            s << ", N=" << header->buffer_number;
            s << ", Size="<< size;
            s << "]";

            return s.str();
        }

};

int read_length_prefixed(std::fstream &f, char* &dst){
    char szbuf[4];
    if(!f.read(szbuf, 4)){
        return 0;
    }
    int size = *((int*) &szbuf);
    if(DEBUG){
        std::cout<<"The size of agent buffer is "<<size<<std::endl;
    }

    if (size < 0 || size > (1024 * 1024 * 100) ){
        std::cout<<"Likely invalid size " << size << " read" << std::endl;
        return 0;
    }

    dst = (char*) malloc(size);
    if (!f.read(dst, size)){
        free(dst);
        dst = nullptr;
        return 0;
    }

    if (DEBUG)
    {
        std::cout<<"Buffer contents are: "<< dst << std::endl;
    }
    
    return size;
}
void read_next_buffer(std::fstream &f){
    char* agentbuf;
    int value = read_length_prefixed(f, agentbuf);
}

void read_buffers(std::string filename){
    std::fstream dataset_fd(filename, std::ios_base::in);

    dataset_fd.seekg(0, std::ios::end);
    size_t length = dataset_fd.tellg();
    dataset_fd.seekg(0, std::ios::beg);

    if(DEBUG){
        std::cout << filename << " has length " << length << std::endl;
    }
    while (dataset_fd.peek() != EOF)
    {
        read_next_buffer(dataset_fd);
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