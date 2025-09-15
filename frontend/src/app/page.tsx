import Image from "next/image";

export default function Home() {
  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={180}
          height={38}
          priority
        />
        <ol className="font-mono list-inside list-decimal text-sm/6 text-center sm:text-left">
          <li className="mb-2 tracking-[-.01em]">
            Get started by editing{" "}
            <code className="bg-black/[.05] dark:bg-white/[.06] font-mono font-semibold px-1 py-0.5 rounded">
              src/app/page.tsx
            </code>
            .
          </li>
          <li className="tracking-[-.01em]">
            Save and see your changes instantly.
          </li>
        </ol>

        <div className="flex gap-2 items-center flex-wrap">
          <a className="rounded border px-3 py-2 text-sm hover:bg-gray-100" href="/dashboard">Dashboard</a>
          <a className="rounded border px-3 py-2 text-sm hover:bg-gray-100" href="/upload">Upload</a>
          <a className="rounded border px-3 py-2 text-sm hover:bg-gray-100" href="/questions">Questions</a>
          <a className="rounded border px-3 py-2 text-sm hover:bg-gray-100" href="/practice">Practice</a>
          <a className="rounded border px-3 py-2 text-sm hover:bg-gray-100" href="/applications">Applications</a>
        </div>
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center text-sm text-gray-500">
        JobPrep AI MVP
      </footer>
    </div>
  );
}
