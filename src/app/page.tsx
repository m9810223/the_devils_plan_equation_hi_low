'use client'

import {useState, useEffect, useRef} from 'react'
import {PythonProvider, usePython} from 'react-py'

type DiffCalcResultT = Array<[number, Array<[string, number]>]>

type DiffCalcResultProps = {dcrs: DiffCalcResultT}

function DiffCalcResult({dcrs}: DiffCalcResultProps) {
    return dcrs.map(([d, cr]) => (
        <>
            <p>±{d}</p>
            {cr.map(([c, r]) => (
                <p key={c}>
                    {c} = {r}
                </p>
            ))}
            <br />
        </>
    ))
}

export default function Page() {
    const {runPython, stdout, stderr, isLoading, isReady, isRunning} = usePython()
    const [mainCode, setMainCode] = useState({})

    const nums_ref = useRef<HTMLInputElement>(null)
    const sign_ref = useRef<HTMLInputElement>(null)
    const sqrt_ref = useRef<HTMLInputElement>(null)

    const [bigs, setBigs] = useState<DiffCalcResultT>([])
    const [smalls, setSmalls] = useState<DiffCalcResultT>([])

    useEffect(() => {
        fetch('/the_devils_plan_equation_hi_low/main.py')
            .then((res) => res.text())
            .then((mainCode) => {
                setMainCode(mainCode)
                // console.log(mainCode)
            })
    }, [])

    return (
        <PythonProvider packages={{micropip: ['pyodide-http']}}>
            <p>
                符號： /, <input ref={sign_ref} />
                (*+- 三選二)
            </p>
            <p>
                根號： <input type="checkbox" ref={sqrt_ref} />
            </p>
            <p>
                數字 <input ref={nums_ref} />
                (0 ~ 10 選四，空白分隔)
            </p>

            {isRunning ? (
                <p>Running...</p>
            ) : !isReady || isLoading ? (
                <p>Loading...</p>
            ) : (
                <button
                    onClick={async () => {
                        const sign = JSON.stringify('/' + sign_ref?.current?.value.trim())
                        const sqrt = JSON.stringify(JSON.stringify(sqrt_ref?.current?.checked))
                        const nums = JSON.stringify(nums_ref?.current?.value.trim())
                        console.log({sign, sqrt, nums})
                        if (!nums) {
                            return
                        }
                        const code = `js_api(${sign}, ${sqrt}, ${nums}, 5, 2)`
                        console.log('code', code)
                        runPython(mainCode + code)
                        try {
                            const obj = JSON.parse(stdout)
                            setBigs(obj.bigs)
                            setSmalls(obj.smalls)
                        } catch (e) {}
                    }}
                >
                    執行
                </button>
            )}
            <div>
                bigs: <DiffCalcResult dcrs={bigs} />
            </div>

            <div>
                smalls: <DiffCalcResult dcrs={smalls} />
            </div>

            <div>{stderr}</div>
        </PythonProvider>
    )
}
