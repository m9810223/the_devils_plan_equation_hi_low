'use client'

import {PythonProvider} from 'react-py'
import {usePython} from 'react-py'

function Codeblock() {
    const {runPython, stdout, stderr, isLoading, isRunning} = usePython()

    return (
        <>
            {isLoading ? (
                <p>Loading...</p>
            ) : (
                <>
                    <button onClick={() => runPython(`print(123)`)}>run</button>
                    <div>result: {stdout}</div>
                </>
            )}
        </>
    )
}

export default function Home() {
    return (
        <PythonProvider packages={{micropip: ['pyodide-http']}}>
            <main>
                <Codeblock />
            </main>
        </PythonProvider>
    )
}
