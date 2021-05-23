import Head from "next/head";
import Form from "../components/form";
import api from "../utils/api";

export default function Index() {
  const onSubmit = function (data) {
    api
      .submitPaste(data)
      .then((r) => r.json())
      .then(({ id }) => {
        window.location.href += `${id}`;
      });
  };

  return (
    <>
      <Head>
        <title>Pastely</title>
      </Head>

      <Form onSubmit={onSubmit} />
    </>
  );
}
