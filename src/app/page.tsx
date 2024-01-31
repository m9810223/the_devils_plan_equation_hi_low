'use client'

import React, {useState, useEffect, useRef} from 'react'
import {PythonProvider, usePython} from 'react-py'
import Chance from 'chance'
import {
    Button,
    Checkbox,
    Heading,
    HStack,
    Input,
    Table,
    TableContainer,
    Tbody,
    Td,
    Text,
    Th,
    Thead,
    Tr,
    VStack,
} from '@chakra-ui/react'
import styled from '@emotion/styled'
import {DragDropContext, Draggable} from 'react-beautiful-dnd'
import {StrictModeDroppable as Droppable} from './StrictModeDroppable'

const chance = new Chance()

type CalcResultsT = Array<[string, number]>
type DiffCalcResultsT = Array<[number, CalcResultsT]>

type CalcResultsProps = {crs: CalcResultsT}
type DiffCalcResultsProps = {dcrs: DiffCalcResultsT}

function CalcResults({crs}: CalcResultsProps) {
    return (
        <TableContainer>
            <Table>
                <Tbody>
                    {crs.map(([c, r]) => (
                        <Tr key={c}>
                            <Td>{c}</Td>
                            <Td isNumeric>{r}</Td>
                        </Tr>
                    ))}
                </Tbody>
            </Table>
        </TableContainer>
    )
}

function DiffCalcResults({dcrs}: DiffCalcResultsProps) {
    return (
        <TableContainer>
            <Table>
                <Tbody>
                    {dcrs.map(([d, cr]) => (
                        <Tr key={d}>
                            <Td>±{d}</Td>
                            <Td>
                                <CalcResults crs={cr} />
                            </Td>
                        </Tr>
                    ))}
                </Tbody>
            </Table>
        </TableContainer>
    )
}

function Main() {
    // py
    const {runPython, stdout, stderr, isLoading, isRunning} = usePython()
    const [mainCode, setMainCode] = useState({})
    const [showResult, setShowResult] = useState(false)
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
        const sign = JSON.stringify('/' + signRef.current?.value.trim())
        const sqrt = JSON.stringify(JSON.stringify(sqrtRef.current?.checked))
        const nums = JSON.stringify(numsRef.current?.value.trim())
        const m = JSON.stringify(mRef.current?.value.trim())
        const n = JSON.stringify(nRef.current?.value.trim())
        console.log({sign, sqrt, nums, m, n})
        const code = `js_api(${sign}, ${sqrt}, ${nums}, ${m}, ${n})`
        console.log('code', code)
        runPython(mainCode + code)
        setShowResult(true)
    }
    const shuffle = () => {
        signRef.current && (signRef.current.value = chance.unique(chance.character, 2, {pool: '+-*'}).join(''))
        sqrtRef.current && (sqrtRef.current.checked = chance.bool())
        numsRef.current && (numsRef.current.value = chance.unique(chance.integer, 4, {min: 0, max: 10}).join(' '))
        setShowResult(false)
    }
    // render
    return (
        <>
            <VStack align="stretch">
                <HStack>
                    <Text>sign:</Text>
                    <Text>/ and</Text>
                    <Input width="auto" ref={signRef} placeholder="*+- 三選二" defaultValue="+*" />
                </HStack>
                <HStack>
                    <Text>sqrt:</Text>
                    <Checkbox ref={sqrtRef} size="lg"></Checkbox>
                </HStack>
                <HStack>
                    <Text>nums:</Text>
                    <Input
                        width="auto"
                        ref={numsRef}
                        placeholder="0 ~ 10 選四，空白分隔"
                        defaultValue="0 1 2 10"
                    />
                </HStack>
                <HStack>
                    <Button onClick={shuffle}>shuffle</Button>
                </HStack>
                <HStack>
                    <Text>m:</Text>
                    <Input width="auto" ref={mRef} defaultValue="3" />
                </HStack>
                <HStack>
                    <Text>n:</Text>
                    <Input width="auto" ref={nRef} defaultValue="2" />
                </HStack>
                <HStack>
                    <Button onClick={run} isLoading={isLoading || isRunning}>
                        {isRunning ? 'running...' : 'run'}
                    </Button>
                </HStack>
            </VStack>
            {showResult && (
                <VStack align="stretch">
                    <Heading>Big</Heading>
                    {stdout && <DiffCalcResults dcrs={JSON.parse(stdout).bigs} />}
                    <Heading>Small</Heading>
                    {stdout && <DiffCalcResults dcrs={JSON.parse(stdout).smalls} />}
                    {stderr && <div>stderr: {stderr}</div>}
                </VStack>
            )}
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

const grid = 8

const QuoteItem = styled.div`
    padding: ${grid}px;
`

// function Quote({quote, index}) {
//     return (
//         <>
//             <Draggable draggableId={quote.id} index={index}>
//                 {(provided) => (
//                     <QuoteItem ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
//                         {quote.content}
//                     </QuoteItem>
//                 )}
//             </Draggable>
//         </>
//     )
// }

// function QuoteApp() {
//     const initial = Array.from({length: 10}, (v, k) => k).map((k) => {
//         const custom: Quote = {
//             id: `id-${k}`,
//             content: `Quote ${k}`,
//         }
//         return custom
//     })
//     const [state, setState] = useState({quotes: initial})
//     const reorder = (list, startIndex, endIndex) => {
//         const result = Array.from(list)
//         const [removed] = result.splice(startIndex, 1)
//         result.splice(endIndex, 0, removed)
//         return result
//     }
//     function onDragEnd(result) {
//         if (!result.destination) {
//             return
//         }
//         if (result.destination.index === result.source.index) {
//             return
//         }
//         const quotes = reorder(state.quotes, result.source.index, result.destination.index)
//         setState({quotes})
//     }
//     const QuoteList = React.memo(function QuoteList({quotes}) {
//         return quotes.map((quote: QuoteType, index: number) => (
//             <Quote quote={quote} index={index} key={quote.id} />
//         ))
//     })
//     return (
//         <DragDropContext onDragEnd={onDragEnd}>
//             <Droppable droppableId="list">
//                 {(provided) => (
//                     <div ref={provided.innerRef} {...provided.droppableProps}>
//                         <QuoteList quotes={state.quotes} />
//                         {provided.placeholder}
//                     </div>
//                 )}
//             </Droppable>
//         </DragDropContext>
//     )
// }
