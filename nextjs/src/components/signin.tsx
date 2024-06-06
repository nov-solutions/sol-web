import "../../public/static/css/styles.css";
import { TextInput } from "@tremor/react";

import { FormEvent } from "react";

import Link from "next/link";

export default function SignIn({
  SITE_BASE_DOMAIN,
  signInBG,
  signInCardBG,
  signInLogoFileName,
  signInTitleColor,
  SITE_NAME,
  signInInputLabelTextColor,
  signInInputFieldBG,
  signInInputFieldTextColor,
  signInForgotPasswordTextColor,
  signInFormSubmitButtonColor,
  signInFormSubmitButtonTextColor,
  signInSignUpDescriptionTextColor,
  signInSignUpAnchorTextColor,
}: {
  SITE_BASE_DOMAIN: string;
  signInBG: string;
  signInCardBG: string;
  signInLogoFileName: string;
  signInTitleColor: string;
  SITE_NAME: string;
  signInInputLabelTextColor: string;
  signInInputFieldBG: string;
  signInInputFieldTextColor: string;
  signInForgotPasswordTextColor: string;
  signInFormSubmitButtonColor: string;
  signInFormSubmitButtonTextColor: string;
  signInSignUpDescriptionTextColor: string;
  signInSignUpAnchorTextColor: string;
}) {

  const signIn = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const signInForm = event.currentTarget;
    const signInFormData = new FormData(signInForm);
    const data = {
      email: signInFormData.get("email"),
      password: signInFormData.getAll("password"),
    };

    const response = await fetch(SITE_BASE_DOMAIN + "/api/sign-in", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    // const result = await response.json();

  }

  return (
    <div className={"flex flex-col flex-grow justify-center px-4 lg:px-0 " + signInBG}>
      <div className={"flex flex-col p-8 mx-auto space-y-8 border-2 rounded-lg border-gray-light lg:w-1/5 " + signInCardBG}>
        <div className="flex flex-col mx-auto">
          <Link href="/" className="w-1/5 place-self-center">
            <img src={"/static/assets/img/logos/" + signInLogoFileName} alt={SITE_NAME + " logo"} />
          </Link>
        </div>
        <h1 className={"text-xl text-center font-semibold " + signInTitleColor}>Sign in to {SITE_NAME}</h1>
        <form className="flex flex-col w-full mx-auto space-y-4 text-sm">
          <div className="space-y-2">
            <label htmlFor="email" className={"font-semibold " + signInInputLabelTextColor}>
              Email
            </label>
            <TextInput required type="email" id="email" name="email" placeholder="" className={"rounded-lg " + signInInputFieldBG + " " + signInInputFieldTextColor} />
          </div>
          <div className="space-y-2">
            <label htmlFor="password" className={"flex justify-between font-semibold " + signInInputLabelTextColor}>
              Password
              <Link href="/app/password-reset" className={"font-semibold text-opacity-50 lg:hover:text-opacity-100 " + signInForgotPasswordTextColor}>
                Forgot your password?
              </Link>
            </label>
            <TextInput required type="password" id="password" name="password" placeholder="" className={"rounded-lg " + signInInputFieldBG + " " + signInInputFieldTextColor} />
          </div>
          <button type="submit" className={"btn " + signInFormSubmitButtonColor + " " + signInFormSubmitButtonTextColor}>
            Sign in
          </button>
        </form>
        <p className={"text-sm " + signInSignUpDescriptionTextColor}>New to {SITE_NAME}?&nbsp;
          <Link href="/app/sign-up" className={"font-semibold text-opacity-50 lg:hover:text-opacity-100 " + signInSignUpAnchorTextColor }>
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}
