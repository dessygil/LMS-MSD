import Link from "next/link";

export default function Home() {
  return (
    <>
      <div className="flex flex-col items-center justify-center h-screen gap-4">
        <div className="font-semibold">LMS-MSD - LANDING</div>
        <Link className="w-1/6 px-4 py-2 rounded-lg bg-green-600 hover:bg-green-800 text-white text-center" href="http://app.localhost:3001">LMS-MSD - APP</Link>
        <Link
          className="w-1/6 px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-800 text-white text-center"
          href="http://api.localhost:8000/api/public"
        >
          Django Public
        </Link>
        <Link
          className="w-1/6 px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-800 text-white text-center"
          href="http://app.localhost:3001/api/session/token"
        >
          Django Private
        </Link>
      </div>
    </>
  );
}
