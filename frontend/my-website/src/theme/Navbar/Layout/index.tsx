/**
 * Custom Navbar Layout
 * Wraps the original Docusaurus Navbar Layout without modifications
 */

import React from "react";
import OriginalNavbarLayout from "@theme-original/Navbar/Layout";
import type { Props } from "@theme/Navbar/Layout";

export default function NavbarLayout(props: Props): JSX.Element {
  return <OriginalNavbarLayout {...props} />;
}
