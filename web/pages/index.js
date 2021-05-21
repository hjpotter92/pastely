import Head from "next/head";
import Form from "../components/form";

export default function Index() {
  const onSubmit = console.log;

  return (
    <>
      <Head>
        <title>Pastely</title>
      </Head>

      <Form onSubmit={onSubmit} />
    </>
  );
}
