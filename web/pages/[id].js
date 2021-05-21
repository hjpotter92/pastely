import { useEffect } from "react";
import Head from "next/head";
import { useRouter } from "next/router";
import retrievePaste from "../utils/api";

export default function PastelyId({ data }) {
  const router = useRouter();
  console.log(data);
  const {
    title,
    shortener: isShorten,
    content,
    created_at,
    expiry,
    id,
    syntax,
  } = data;
  useEffect(() => {
    if (isShorten) {
      router.push(content);
    }
  });
  return (
    <>
      {title && (
        <Head>
          <title>{title} - Pastely</title>
        </Head>
      )}
      <div>
        <div>{id}</div>
        <div>{created_at}</div>
        {expiry && <div>{expiry}</div>}
        <div className="float-right">Copy | Download | Raw | New</div>
        <div className="float-left font-bold text-xl">
          {title} {syntax && `(${syntax})`}
        </div>
        <div className="clear-both"></div>
        <pre className="font-mono">
          <code>{content}</code>
        </pre>
      </div>
    </>
  );
}

export async function getServerSideProps(context) {
  const { id } = context.params;
  const data = await retrievePaste.retrievePaste(id);
  return { props: { data } };
}
