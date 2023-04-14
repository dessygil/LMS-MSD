import { handleAuth, handleLogin } from '@auth0/nextjs-auth0';

export default handleAuth({
    login: handleLogin({
        authorizationParams: {
            audience: process.env.NEXT_PUBLIC_AUTH0_AUDIENCE,
        }
    })
});
