import Link from "next/link";
import { withPageAuthRequired } from "@auth0/nextjs-auth0";

export default function Dashboard({ user }) {
    return (
      <div>
        Welcome {user.name}! <Link href="/api/auth/logout">Logout</Link>
      </div>
    );
  }
  
  export const getServerSideProps = withPageAuthRequired();
