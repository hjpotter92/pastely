import Document, { Html, Head, Main, NextScript } from "next/document";
import Header from "../components/header";
import Footer from "../components/footer";

export default class PastelyDocument extends Document {
  render() {
    return (
      <Html lang="en">
        <Head></Head>
        <body className="container mx-auto">
          <Header />
          <Main />
          <NextScript />
          <Footer />
        </body>
      </Html>
    );
  }
}
