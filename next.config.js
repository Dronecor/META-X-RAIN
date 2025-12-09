/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        remotePatterns: [
            {
                protocol: 'https',
                hostname: 'pollinations.ai',
                pathname: '/p/**',
            },
        ],
    },
}

module.exports = nextConfig
