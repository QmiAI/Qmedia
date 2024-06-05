import Header from "@/components/header";
import Sidebar from "@/components/sidebar";
import Gallery from "@/components/gallery";
import Tabs from "@/components/tabs";

export default function Home() {
  return (
    <>
      <div className="fixed w-screen 2xl:container mx-auto left-1/2 transform -translate-x-1/2 z-10">
        <Header />
      </div>
      <div className="dark:bg-inherit 2xl:container mx-auto relative flex">
        <Sidebar />
        <main className="pt-24 pl-6 lg:pl-0 pr-6 2xl:pr-0 flex-1">
          <Tabs />
          <div className="mb-4" />
          <Gallery />
          <footer className="mt-24"></footer>
        </main>
      </div>
    </>
  );
}
