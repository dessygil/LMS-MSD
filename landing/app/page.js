import Link from "next/link";

export default function Home() {
  return (
    <>
      <div>LMS-MSD - LANDING</div>
      <Link href="http://app.localhost:3001">APP</Link>
      <br />
      <Link href="http://api.localhost:8000/api/private">Django Private API</Link>
    </>
  );
}
