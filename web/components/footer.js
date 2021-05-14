import Link from "next/link";
import Favicon from "../public/favicon.svg";

export default function Footer() {
  return (
    <>
      <footer className="h-12 bg-gray-600 text-gray-50 relative inset-x-0 bottom-0 flex grid grid-cols-2 items-center content-center mt-4">
        <div className="m-8">
          <Favicon className="object-cover object-center float-left mr-4 fill-current" />
          <Link href="/">Pastely</Link>
        </div>
        <div className="m-8 justify-self-end flex gap-4">
          <Link href="/about">About</Link>
          <Link href="https://github.com/hjpotter92/pastely">GitHub</Link>
        </div>
      </footer>
    </>
  );
}
