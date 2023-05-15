import React from 'react'
import Link from 'next/link'
import { useUser } from '@auth0/nextjs-auth0/client'
import { useRouter } from 'next/router'

function login() {
  const { user } = useUser()
  const router = useRouter()

  if (user) {
    router.push('/dashboard')
    return null
  }
  return (
    <>
      <div className="flex flex-col items-center justify-center h-screen gap-4">
        <Link
          className="w-1/6 px-4 py-2 rounded-lg bg-green-600 hover:bg-green-800 text-white text-center"
          href="/api/auth/login"
        >
          Login
        </Link>
        <Link
          className="w-1/6 px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-800 text-white text-center"
          href="http://api.localhost:8000/api/public"
        >
          Django Public
        </Link>
        <Link
          className="w-1/6 px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-800 text-white text-center"
          href="/api/session/token"
        >
          Django Private
        </Link>
      </div>
    </>
  )
}

export default login
