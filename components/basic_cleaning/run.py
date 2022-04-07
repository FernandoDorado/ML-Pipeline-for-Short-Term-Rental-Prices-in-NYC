#!/usr/bin/env python
"""
An example of step using MLFlow and W&B
"""
import argparse
import logging
import wandb
import pandas as pd
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info("Downloading artifacts")
    artifact_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_path)


    logger.info("Removing outliers")
    # Calculate index to drop
    idx = df['price'].between(args.min_price, args.max_price)
    # Drop rows by index (idx)
    df = df[idx].copy()

    # Transform column to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Keep rows between desired lat/long
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    # Save artifacts
    logger.info("Save the generated artifact")
    file_name = "clean_sample.csv"
    df.to_csv(file_name, index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(file_name)
    run.log_artifact(artifact)

    os.remove(file_name)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Name of the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price in order to clean outliers",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum price in order to clean outliers",
        required=True
    )


    args = parser.parse_args()

    go(args)
