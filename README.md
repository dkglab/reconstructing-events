# Reconstructing Events

## Setup

### Make your copy of the Google sheet

1. Open the [Reconstructing Events Google
sheet](https://docs.google.com/spreadsheets/d/1memmdLOAsgAHJqrMrXjGbh7_R9VV-iDk6XJMN5Qg8Gc/edit?usp=sharing)
and make your own copy of it.

1. Make sure your copy of the sheet is named `Reconstructing Events`,
   not `Reconstructing Events copy` or some other variation.

1. Share your sheet with
   `import-triples@import-triples.iam.gserviceaccount.com` as a
   viewer.

### Open your codespace

1. Go to the [Reconstructing Events GitHub repository](https://github.com/dkglab/reconstructing-events).

1. Click the green "Code" button and select "Open with Codespaces",
   then "New codespace".

1. Wait for the codespace to finish setting up.

## Creating triples and running inference

1. In your sheet, create triples describing your event.

1. The first time you click one of the buttons to add triples in the
   sheet, you will get a scary warning! Don't worry, you can trust me
   :^)

1. In your codespace, open a terminal and run:

   ```bash
   make triples.ttl
   ```

1. In your codespace file explorer, open `triples.ttl` to see the
   triples you wrote.

1. In your codespace terminal, run:

   ```bash
   make events.ttl
   ```

1. In your codespace file explorer, open `events.ttl` to see the
   triples you wrote plus additional inferred triples.

## Visualizing events

1. In your codespace file explorer, right-click or control-click on
   `events.ttl` and select "Download".

1. Go to <https://spaestiem.fly.dev/> and click "Choose RDF event data
   to load" and choose the `events.ttl` file you just downloaded.
