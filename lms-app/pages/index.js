import { useUser } from "@auth0/nextjs-auth0/client";
import { useRouter } from "next/router";

function Home() {
  const { user, error, isLoading } = useUser();
  const router = useRouter();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error.message}</div>;
  }

  if (user) {
    router.push("/dashboard");
    return null;
  }

  if (!user) {
    router.push("/auth/login");
  }

  return null;
}

export default Home;
