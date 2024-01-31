import type {Metadata} from 'next'
import {Providers} from './providers'
import {fonts} from './fonts'

export const metadata: Metadata = {
    title: '尊嚴白隊',
}

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode
}>) {
    return (
        <html className={fonts.rubik.variable}>
            <body>
                <Providers>{children}</Providers>
            </body>
        </html>
    )
}
