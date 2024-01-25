'use client'

import {PythonProvider} from 'react-py'

import Codeblock from './components/Codeblock'

export default function Home() {
    return (
        <PythonProvider packages={{micropip: ['pyodide-http']}}>
            <main>
                <Codeblock />
            </main>
        </PythonProvider>
    )
}
