pub mod jaeger_trace;
use pyo3::{prelude::*, types::PyDict};
use jaeger_trace::JRoot;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn heimdall_jaeger_parse(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<JRoot>()?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}