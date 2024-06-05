import { getRagQuery } from "@/lib/api";
import Text from "./answers-text";

export default async function Page({
  searchParams,
  className,
}: {
  searchParams: { q: string };
  className?: string;
}) {
  const res = await getRagQuery(searchParams.q, { backend: true });
  const llmAnswer = String(await res.query_response).replace(/\s\\n\s/g, "\n");
  // const llmAnswer = `abcdefg`; // for testing

  return <Text className={className} text={llmAnswer} />;
}
