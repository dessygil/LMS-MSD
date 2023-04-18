import React from "react";
import { useUser } from "@auth0/nextjs-auth0/client";



export default function testEndpoint() {
    const { user } = useUser();
    console.log(user);
    return (
        <>
            {user ? <p>{user.email}</p>: <p>not logged in</p>}
        </>
    );
}
