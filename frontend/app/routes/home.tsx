import type { Route } from "./+types/home";
import { Test } from "~/components/test";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "jarvis" },
    { name: "description", content: "welcome master!!" },
  ];
}

export default function Home() {
  return <Test/>;
}
