import Head from "next/head";
import { useForm } from "react-hook-form";

export default function Index() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm();
  const watchShortener = watch("shortener", false);
  const watchProtect = watch("protect", false);

  const onSubmit = console.log;

  return (
    <>
      <Head>
        <title>Pastely</title>
      </Head>
      {JSON.stringify(errors)}
      <form onSubmit={handleSubmit(onSubmit)}>
        <fieldset>
          <legend>URL Shortener</legend>
          <label className={(watchShortener && "checked") || "unchecked"}>
            <input id="shortener" {...register("shortener")} type="checkbox" />
            <span>Only shorten a single URL</span>
          </label>
          {watchShortener && (
            <input id="shorten" {...register("shorten")} type="text" />
          )}
        </fieldset>

        <fieldset>
          <legend>Text snippet</legend>
          <div className="grid grid-cols-2 gap-4">
            <input
              id="title"
              type="text"
              {...register("title")}
              required
              placeholder="Snippet title"
            />
            <input
              id="syntax"
              type="text"
              {...register("syntax")}
              placeholder="Syntax highlight"
            />
            <textarea
              cols="120"
              id="content"
              rows="10"
              placeholder="lorem"
              className="resize w-full col-span-2"
              {...register("content")}
            ></textarea>
          </div>
        </fieldset>

        <fieldset>
          <legend>Encrypt snippet/redirect</legend>
          <label className={(watchProtect && "checked") || "unchecked"}>
            <input type="checkbox" {...register("protect")} />
            <span>Protect/encrypt content with passphrase</span>
          </label>
          {watchProtect && (
            <input
              id="text"
              type="text"
              placeholder="passphrase"
              {...register("passphrase")}
            />
          )}
        </fieldset>

        <fieldset>
          <legend>Expiry</legend>
          <label>
            Set expiry duration for the snippet
            <select id="expiry" {...register("expiry")}>
              <option value="0" selected>
                Never expire
              </option>
              <option value="1">1 hour</option>
              <option value="2">2 hours</option>
              <option value="6">6 hours</option>
              <option value="12">12 hours</option>
              <option value="24">1 day</option>
              <option value="144">1 week</option>
              <option value="288">2 weeks</option>
              <option value="730">1 month</option>
              <option value="1460">2 months</option>
              <option value="4383">6 months</option>
              <option value="8766">1 year</option>
            </select>
          </label>
        </fieldset>
        <input name="submit" type="submit" />
      </form>
    </>
  );
}
