import "../styles/globals.css";
import React from "react";
import { UserProvider } from "@auth0/nextjs-auth0/client";
import { QueryClientProvider, QueryClient } from "react-query";

const queryClient = new QueryClient();

export default function App({ Component, pageProps }) {
  return (
    <UserProvider>
      <QueryClientProvider client={queryClient}>
        <Component {...pageProps} />
      </QueryClientProvider>
    </UserProvider>
  );
}
