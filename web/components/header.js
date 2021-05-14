import Link from "next/link";
import Favicon from "../public/favicon.svg";

export default function Header() {
  return (
    <>
      <nav className="h-12 bg-gray-600 text-gray-50 sticky top-0 mb-4 flex grid grid-cols-2 items-center content-center">
        <div className="p-8">
          <Favicon className="object-cover object-center float-left mr-4 fill-current" />
          <Link href="/">Pastely</Link>
        </div>
        <div className="justify-self-end p-8 flex gap-4">
          <Link href="/about">About</Link>
          <Link href="https://github.com/hjpotter92/pastely">GitHub</Link>
        </div>
      </nav>
    </>
  );
}
