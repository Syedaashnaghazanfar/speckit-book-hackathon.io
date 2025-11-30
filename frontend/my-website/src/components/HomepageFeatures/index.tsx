import type { ReactNode } from "react";
import clsx from "clsx";
import Heading from "@theme/Heading";
import styles from "./styles.module.css";

type FeatureItem = {
  title: string;
  imgSrc: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: "ROS 2 Fundamentals",
    imgSrc: require("@site/static/img/artificial-intelligence.png").default,
    description: (
      <>
        Master the Robotic Operating System that powers modern robots. Learn
        nodes, topics, services, and advanced patterns for building intelligent
        robotic systems.
      </>
    ),
  },
  {
    title: "Robot Simulation",
    imgSrc: require("@site/static/img/ai-technology.png").default,
    description: (
      <>
        Build and test robots in Gazebo before deploying to real hardware.
        Create URDF models, simulate physics, and integrate sensors in a safe
        virtual environment.
      </>
    ),
  },
  {
    title: "AI-Powered Intelligence",
    imgSrc: require("@site/static/img/ai.png").default,
    description: (
      <>
        Leverage NVIDIA Isaac and Vision-Language-Action models for perception,
        navigation, and manipulation. Deploy AI to Jetson edge devices for
        autonomous operation.
      </>
    ),
  },
];

function Feature({ title, imgSrc, description }: FeatureItem) {
  return (
    <div className={clsx("col col--4")}>
      <div className="text--center">
        <img
          src={imgSrc}
          className={styles.featureSvg}
          role="img"
          alt={title}
          style={{
            borderRadius: "12px",
            maxHeight: "200px",
            objectFit: "contain",
          }}
        />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3" className="highlight-purple">
          {title}
        </Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
