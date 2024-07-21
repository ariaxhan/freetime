import * as React from "react";

function LandingPage() {
  return (
    <div className="flex flex-col justify-center text-7xl bg-neutral-200 text-zinc-950 max-md:text-4xl">
      <div className="flex flex-col justify-center w-full bg-white max-md:max-w-full max-md:text-4xl">
        <div className="flex overflow-hidden relative flex-col items-center px-16 pt-11 pb-20 w-full h-screen fill-[url(<path-to-image>)_lightgray_0px_-514px_/_100%_190.813%_no-repeat] min-h-[1024px] max-md:px-5 max-md:max-w-full max-md:text-4xl">
          <img
            loading="lazy"
            srcSet="..."
            className="object-cover absolute inset-0 size-full"
          />
          <div className="flex relative flex-col items-center mb-52 max-w-full w-[842px] max-md:mb-10 max-md:text-4xl">
            <img
              loading="lazy"
              srcSet="..."
              className="max-w-full aspect-[3.57] w-[344px]"
            />
            <div className="self-stretch mt-24 h-auto text-center grow-0 max-md:mt-10 max-md:max-w-full max-md:text-4xl max-sm:self-center max-sm:pr-11">
              <blockquote className="p-0 my-0 mr-0 ml-10 border-[none]">
                <h4>
                  <span className="self-center text-right font-[normal]">
                    <span className="text-left">
                      <span className="text-center">
                        <span>
                          Plan less, connect more,
                          <br />
                        </span>
                      </span>
                    </span>
                  </span>
                  <span className="self-center text-right font-[normal]">
                    <span className="text-left">
                      <span className="text-center">
                        <span>and meet new people</span>
                      </span>
                    </span>
                  </span>
                </h4>
              </blockquote>
            </div>
            <div className="mt-px text-3xl text-center max-md:mt-10 max-md:max-w-full max-sm:mt-0 max-sm:mr-auto">
              <h4>
                <span className="font-[normal]">
                  Elevates your social life with small, curated gatherings.
                </span>
              </h4>
            </div>
            <div className="flex overflow-hidden relative flex-col justify-center px-14 py-6 mt-36 text-2xl text-white aspect-[3.36] fill-violet-500 max-md:px-5 max-md:mt-10">
              <img
                loading="lazy"
                src="https://cdn.builder.io/api/v1/image/assets/TEMP/f1d9bdd013f4dc7f449feb14ec61a5e06a9dcc4d84e60da7c21cd61807295b7c?"
                className="object-cover absolute inset-0 size-full"
              />
              Get started
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;
