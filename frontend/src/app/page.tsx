import ChatWidget from "./components/ChatWidget";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-zinc-50 px-6 font-sans dark:bg-black">
      <main className="flex max-w-2xl flex-col items-center gap-4 text-center">
        <h1 className="text-3xl font-semibold tracking-tight text-black dark:text-zinc-50">
          Hi, I&apos;m Plamen.
        </h1>
        <p className="text-lg leading-8 text-zinc-600 dark:text-zinc-400">
          Ask my portfolio assistant about my projects, stack, or availability using
          the chat button in the corner.
        </p>
      </main>
      <ChatWidget />
    </div>
  );
}
