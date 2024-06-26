import "../../public/static/css/styles.css";
import { TextInput } from "@tremor/react";

import { FormEvent } from "react";

import Link from "next/link";

export default function SignUp({
  SITE_BASE_DOMAIN,
  signUpBG,
  signUpCardBG,
  signUpLogoFileName,
  signUpTitleColor,
  SITE_NAME,
  signUpInputLabelTextColor,
  signUpInputFieldBG,
  signUpInputFieldTextColor,
  signUpFormSubmitButtonColor,
  signUpFormSubmitButtonTextColor,
  signUpSignInDescriptionTextColor,
  signUpSignInAnchorTextColor,
}: {
  SITE_BASE_DOMAIN: string;
  signUpBG: string;
  signUpCardBG: string;
  signUpLogoFileName: string;
  signUpTitleColor: string;
  SITE_NAME: string;
  signUpInputLabelTextColor: string;
  signUpInputFieldBG: string;
  signUpInputFieldTextColor: string;
  signUpFormSubmitButtonColor: string;
  signUpFormSubmitButtonTextColor: string;
  signUpSignInDescriptionTextColor: string;
  signUpSignInAnchorTextColor: string;
}) {

  const signUp = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const signUpForm = event.currentTarget;
    const signUpFormData = new FormData(signUpForm);
    const data = {
      email: signUpFormData.get("email"),
      password: signUpFormData.getAll("password"),
    };

    const response = await fetch(SITE_BASE_DOMAIN + "/api/sign-up", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    // const result = await response.json();

  }

  return (
    <div className={"flex flex-col flex-grow justify-center px-4 lg:px-0 " + signUpBG}>
      <div className={"flex flex-col p-8 mx-auto space-y-8 border-2 rounded-lg border-gray-light lg:w-1/5 " + signUpCardBG}>
        <div className="flex flex-col mx-auto">
          <Link href="/" className="w-1/5 place-self-center">
            <img src={"/static/assets/img/logos/" + signUpLogoFileName} alt={SITE_NAME + " logo"} />
          </Link>
        </div>
        <h1 className={"text-xl text-center font-semibold " + signUpTitleColor}>Sign up for {SITE_NAME}</h1>
        <form onSubmit={signUp} className="flex flex-col w-full mx-auto space-y-4 text-sm">
          <div className="space-y-2">
            <label htmlFor="email" className={"font-semibold " + signUpInputLabelTextColor}>
              Email
            </label>
            <TextInput required type="email" id="email" name="email" placeholder="" className={"rounded-lg " + signUpInputFieldBG + " " + signUpInputFieldTextColor} />
          </div>
          <div className="space-y-2">
            <label htmlFor="password" className={"font-semibold " + signUpInputLabelTextColor}>
              Password
            </label>
            <TextInput required type="password" id="password" name="password" placeholder="" className={"rounded-lg " + signUpInputFieldBG + " " + signUpInputFieldTextColor} />
          </div>
          <button type="submit" className={"btn " + signUpFormSubmitButtonColor + " " + signUpFormSubmitButtonTextColor}>
            Sign up
          </button>
        </form>
        <p className={"text-sm " + signUpSignInDescriptionTextColor}>Already have an account?&nbsp;
          <Link href="/app/sign-in" className={"font-semibold text-opacity-50 lg:hover:text-opacity-100 " + signUpSignInAnchorTextColor }>
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
