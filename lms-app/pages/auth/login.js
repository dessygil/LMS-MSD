import React from "react";
import Link from "next/link";
import { useUser } from "@auth0/nextjs-auth0/client";
import { useRouter } from "next/router";

function login() {
  const { user } = useUser();
  const router = useRouter();

  if (user) {
    router.push("/dashboard");
    return null;
  }
  return (
    <>
      <Link href="/api/auth/login">Login</Link>
      <br />
      <Link href="/api/hello">Hello (Next.JS API Route Example)</Link>
      <br />
      <Link href="http://api.localhost:8000/api/private">Django Private API</Link>
    </>
  );
}

export default login;
