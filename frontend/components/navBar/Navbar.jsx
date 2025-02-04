"use client";

import UserProfile from "../userProfile/UserProfile";
import styles from "./navbar.module.css";
import Image from "next/image";
import { useState } from "react";
import InfoWizard from "../InfoWizard/InfoWizard";

const Navbar = () => {
  const [openHelpModal, setOpenHelpModal] = useState(false);
  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>
        <Image src="/assets/logo.png" alt="Logo" width={200} height={40} />{" "}
      </div>
      <InfoWizard
          open={openHelpModal}
          setOpen={setOpenHelpModal}
          tooltipText="Tell me more!"
          iconGlyph="Wizard"
          sections={[
            {
              heading: "Instructions and Talk Track",
              content: [
                {
                  heading: "What is Open Finance?",
                  body: "Open Finance refers to the concept of allowing customers to securely share their financial data with third parties, beyond traditional banking services, to enable a broader range of financial products and services. It builds upon the principles of Open Banking, which focuses primarily on bank accounts, but extends the scope to include other financial products such as investments, insurance, pensions, and loans.",
                },
                {
                  heading: "How to Demo",
                  body: [
                    "Click on the “Connect Bank” button",
                    "Select a fictional bank you would like to connect from the dropdown",
                    "Allow the modal to go through the different steps",
                    "Once the connection is completed you should see the new accounts or products displayed alongside your Leafy Bank accounts, with a blue badge indicating the name of the new bank.",
                    "Your “Global Position” will also be updated accordingly following these changes.",
                    "If you wish to remove a specific account/product from your list, click on the disconnect icon on the card. This card will disappear from your view, and the amount will be discounted from the global position totals."
                  ],
                },
              ],
            },
            {
              heading: "Behind the Scenes",
              content: [
                {
                  heading: "Data Flow",
                  body: "",
                },
                {
                  image: {
                    src: "./OF_info.png",
                    alt: "Architecture",
                  },
                },
              ],
            },
            {
              heading: "Why MongoDB?",
              content: [
                {
                  heading: "Flexibility",
                  body: "MongoDB shines in its flexibility—serving as a central data storage solution for retrieving data from external financial institutions while seamlessly supporting diverse formats and structures.",
                },
              ],
            },
          ]}
        />
      <div className={styles.user}>
        <UserProfile />
      </div>
    </nav>
  );
};

export default Navbar;
