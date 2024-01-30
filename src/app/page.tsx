'use client'

import {useState, useEffect, useRef} from 'react'
import {PythonProvider, usePython} from 'react-py'

type DiffCalcResultT = Array<[number, Array<[string, number]>]>

type DiffCalcResultProps = {dcrs: DiffCalcResultT}

function DiffCalcResult({dcrs}: DiffCalcResultProps) {
    return dcrs.map(([d, cr]) => (
        <div key={d}>
            <p>±{d}</p>
            {cr.map(([c, r]) => (
                <p key={c}>
                    {c} = {r}
                </p>
            ))}
            <br />
        </div>
    ))
}

function Main() {
    // py
    const {runPython, stdout, stderr, isLoading, isRunning} = usePython()
    const [mainCode, setMainCode] = useState({})
    // ref
    const numsRef = useRef<HTMLInputElement>(null)
    const signRef = useRef<HTMLInputElement>(null)
    const sqrtRef = useRef<HTMLInputElement>(null)
    const mRef = useRef<HTMLInputElement>(null)
    const nRef = useRef<HTMLInputElement>(null)
    // init
    useEffect(() => {
        fetch('/the_devils_plan_equation_hi_low/main.py')
            .then((res) => res.text())
            .then((code) => {
                setMainCode(code)
                // console.log(code)
            })
    }, [])
    // handler
    const run = () => {
        const sign = JSON.stringify('/' + signRef?.current?.value.trim())
        const sqrt = JSON.stringify(JSON.stringify(sqrtRef?.current?.checked))
        const nums = JSON.stringify(numsRef?.current?.value.trim())
        const m = JSON.stringify(mRef?.current?.value.trim())
        const n = JSON.stringify(nRef?.current?.value.trim())
        console.log({sign, sqrt, nums, m, n})
        const code = `js_api(${sign}, ${sqrt}, ${nums}, ${m}, ${n})`
        console.log('code', code)
        runPython(mainCode + code)
    }
    // render
    return (
        <>
            <p>
                符號： {`'/'`} and <input ref={signRef} defaultValue="+*" placeholder="*+- 三選二" />
            </p>
            <p>
                根號： <input type="checkbox" ref={sqrtRef} defaultChecked={false} />
            </p>
            <p>
                數字： <input ref={numsRef} defaultValue="0 1 2 10" placeholder="0 ~ 10 選四，空白分隔" />
            </p>
            <p>
                m: <input ref={mRef} defaultValue="5" />
            </p>
            <p>
                n: <input ref={nRef} defaultValue="1" />
            </p>

            <input
                type="button"
                value={isRunning ? 'running...' : 'run'}
                disabled={isLoading || isRunning}
                onClick={run}
            />

            <br />
            <br />
            <div>
                bigs:
                <br />
                <br />
                {stdout && <DiffCalcResult dcrs={JSON.parse(stdout).bigs} />}
            </div>
            <div>
                smalls:
                <br />
                <br />
                {stdout && <DiffCalcResult dcrs={JSON.parse(stdout).smalls} />}
            </div>
            <br />
            {stderr && <div>stderr: {stderr}</div>}
        </>
    )
}

export default function Page() {
    return (
        <PythonProvider packages={{micropip: ['pyodide-http']}}>
            <Main />
        </PythonProvider>
    )
}
