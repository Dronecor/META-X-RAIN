export const metadata = {
    title: 'ShopBuddy - AI Fashion Assistant',
    description: 'Your personal AI shopping companion',
}

export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <body style={{ margin: 0, padding: 0 }}>{children}</body>
        </html>
    )
}
