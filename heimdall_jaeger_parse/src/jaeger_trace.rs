use pyo3::prelude::*;
use base_storage::data_structure::*;

#[pyclass]
#[derive(Clone, Debug)]
pub struct JReferences{
    #[pyo3(get, set)]
    pub ref_type: String,

    #[pyo3(get, set)]
    pub trace_id: String,

    #[pyo3(get, set)]
    pub span_id: String,
}

#[pymethods]
impl JReferences {
    #[new]
    pub fn new(ref_type: String, trace_id: String, span_id: String) -> Self {
        JReferences { 
            ref_type, 
            trace_id,
            span_id
        }
    }
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct JTags{
    #[pyo3(get, set)]
    pub key: String,

    #[pyo3(get, set)]
    pub type_: String,

    #[pyo3(get, set)]
    pub value: String

}

#[pymethods]
impl JTags{

    #[new]
    pub fn new(key: String, type_: String, value: String) -> Self{
        JTags { 
            key, 
            type_, 
            value
        }
    }
}


#[pyclass]
#[derive(Clone, Debug)]
pub struct JSpan{

    #[pyo3(get, set)]
    pub trace_id: String,

    #[pyo3(get, set)]
    pub span_id: String, 

    #[pyo3(get, set)]
    pub flags: u8,

    #[pyo3(get, set)]
    pub operation_name: String, 

    #[pyo3(get, set)]
    pub references: Vec<Option<JReferences>>,

    #[pyo3(get, set)]
    pub start_time: u128,

    #[pyo3(get, set)]
    pub duration: u128,

    #[pyo3(get, set)]
    pub tags: Vec<JTags>
}

#[pymethods]
impl JSpan{
    #[new]
    pub fn new(trace_id: String, span_id: String, flags: u8, operation_name: String, 
        references: Vec<Option<JReferences>>, start_time: u128, 
        duration: u128, tags: Vec<JTags>) -> JSpan {
        JSpan { 
            trace_id,
            span_id, 
            flags,
            operation_name, 
            references, 
            start_time, 
            duration,
            tags,
        }
    }
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct JData{
    #[pyo3(get, set)]
    pub trace_id: String, 

    #[pyo3(get, set)]
    pub spans: Vec<JSpan>,
}

#[pymethods]
impl JData {
    #[new]
    pub fn new(trace_id: String, spans: Vec<JSpan>) -> JData{
        JData { 
            trace_id,
            spans 
        }
    }
}

#[pyclass]
pub struct JRoot{
    #[pyo3(get, set)]
    pub data: Vec<JData>,

    #[pyo3(get, set)]
    pub total: u64,

    #[pyo3(get, set)]
    pub limit: u64,

    #[pyo3(get, set)]
    pub offset: u64,

    #[pyo3(get, set)] 
    pub errors: Option<String>,
}

#[pymethods]
impl JRoot{
    
    #[new]
    pub fn new(filename: String) -> JRoot{
        let jaeger_root = base_storage::jaeger_parser(filename);
        let mut jdata_vec: Vec<JData> = Vec::new();
        for jdata in jaeger_root.data{
            let jspans = convert_to_jspan(jdata.spans);
            let jd = JData::new(jdata.trace_id, jspans);
            jdata_vec.push(jd);
        }

        JRoot { 
            data: jdata_vec, 
            total: jaeger_root.total, 
            limit: jaeger_root.limit,
            offset: jaeger_root.offset, 
            errors: jaeger_root.errors 
        }
    }

}

pub fn convert_to_jspan(span_data: Vec<Span>) -> Vec<JSpan>{
    let mut jspan_vec: Vec<JSpan> = Vec::new();
    for data in span_data{
        let tag_info = convert_to_jtags(data.tags);
        let reference_info = convert_to_references(data.references);
        let jspan_obj = JSpan::new(
            data.trace_id, data.span_id, data.flags, 
            data.operation_name, reference_info, 
            data.start_time, data.duration, tag_info);
        jspan_vec.push(jspan_obj);
    }
    jspan_vec
}

pub fn convert_to_references(reference_data: Vec<Option<References>>) -> Vec<Option<JReferences>>{

    let mut jref_data: Vec<Option<JReferences>> = Vec::new();
    for data in reference_data{
        let jdata = JReferences::new( data.clone().unwrap().ref_type, data.clone().unwrap().trace_id, data.unwrap().span_id);
        jref_data.push(Some(jdata));
    }

    jref_data

}

pub fn convert_to_jtags(tags_data: Vec<Tags>) -> Vec<JTags>{

    let mut jtags_data: Vec<JTags> = Vec::new();
    for data in tags_data{
        let jtag = JTags::new(data.key, data.type_, data.value);
        jtags_data.push(jtag);
    }
    jtags_data

}