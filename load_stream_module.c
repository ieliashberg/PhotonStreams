
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>

// Our custom load_stream function.
static PyObject * load_stream(PyObject *self, PyObject *args) {
    const char *filename;
    // parse the input tuple to retrieve a C string.
    if(!PyArg_ParseTuple(args, "s", &filename)) {
        return NULL;
    }

    // open the file in binary read mode.
    FILE *fp = fopen(filename, "rb");
    if (!fp) {
        PyErr_SetFromErrnoWithFilename(PyExc_IOError, filename);
       return NULL;
    }

    // seek to the end to determine file size.
    fseek(fp, 0, SEEK_END);
    size_t fsize = (size_t)ftell(fp);
    fseek(fp, 0, SEEK_SET);

    // allocate a buffer for the file content.
    char * buffer = malloc(fsize + 1);
    if (!buffer) {
        fclose(fp);
        return PyErr_NoMemory();
    }
    size_t read_size = fread(buffer, 1, fsize, fp);
    fclose(fp);
    if (read_size != fsize) {
        free(buffer);
        PyErr_SetString(PyExc_IOError, "Error reading file");
        return NULL;
    }
    buffer[fsize] = '\0';

    // allocate a new buffer for filtered data.
    // worst-case size is fsize + 1.
    char * filtered = malloc(fsize + 1);
    if (!filtered) {
        free(buffer);
        return PyErr_NoMemory();
    }
    long j = 0;
    for (size_t i = 0; i < fsize; i++) {
        char c = buffer[i];
        // only copy '0' and '1'
        if (c == '0' || c == '1') {
            filtered[j++] = c;
        }
    }
    filtered[j] = '\0';
    free(buffer);

    // convert the filtered string into a PyLong integer.
    // PyLong_FromString allows conversion with a given base (here, 2).
    PyObject *result = PyLong_FromString(filtered, NULL, 2);
    free(filtered);
    return result;
}
// list of functions defined in this module.
static PyMethodDef LoadStreamMethods[] = {
        {"load_stream", load_stream, METH_VARARGS, "Load a bit stream from file and convert to integer."},
        {NULL, NULL, 0, NULL}  // Sentinel
};

// module definition
static struct PyModuleDef loadstreammodule = {
        PyModuleDef_HEAD_INIT,
        "load_stream_module",  // Module name
        NULL,  // Module documentation, can be NULL
         -1,    // Size of per-interpreter state of the module,
        LoadStreamMethods
};

// module initialization function
PyMODINIT_FUNC PyInit_load_stream_module(void) {
    return PyModule_Create(&loadstreammodule);
}


