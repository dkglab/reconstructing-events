# Reconstructing Events

## Setup

### Make your copy of the Google sheet

1. Open the [Reconstructing Events Google
sheet](https://docs.google.com/spreadsheets/d/1memmdLOAsgAHJqrMrXjGbh7_R9VV-iDk6XJMN5Qg8Gc/edit?usp=sharing)
and make your own copy of it.

### Open your codespace

1. Go to the [Reconstructing Events GitHub repository](https://github.com/dkglab/reconstructing-events).

1. Click the green "Code" button and select "Open with Codespaces",
   then "New codespace".

1. Wait for the codespace to finish setting up.

## Creating triples and running inference

### Create your triples in the sheet

1. In your sheet, create triples describing your event.

1. The first time you click one of the buttons to add triples in the
   sheet, you will get a scary warning. The “Add Triples” script you
   will be asked to authorize just takes some text you type into the
   forms on the right and formats it properly as triples for insertion
   into the table on the left.

1. The forms are just for convenience; you can edit and copy and paste
   values among the rows of triples as normal.

### Import the triples into your codespace

1. In your codespace, open a terminal and run:

   ```bash
   make triples.ttl
   ```

1. The first time you run `make triples.ttl`, a browser tab will open
   and you will be prompted to authorize Import Triples to read the
   names of files in your Google Drive, and to read data in your
   Google Sheets. This **only** grants access to your data when
   **you** run the script, not other people.

1. Because this is not a commercially published app, it has not been
   “verified” by Google, so you will need to click through a few
   scary-looking notices and on “advanced” settings to finish
   authorizing the script. On subsequent runs, you won't need to do
   this.

1. After you’ve finished consenting to data access, Google will try to
   redirect your browser back to your local machine. But since you are
   running in a codespace, this will fail. This is OK and
   expected. When you see the browser fail to connect to `localhost`,
   copy the URL out of the address bar. It will look something like
   this (but with much longer strings in place of `XXX`, `YYY`, and
   `ZZZ`:

   `http://localhost/?state=XXX&code=YYY&scope=ZZZ`

1. Switch back to the browser tab that your codespace is in, and paste
   the URL you copied into the terminal.

1. The script should finish creating `triples.ttl`.

1. In your codespace file explorer, open `triples.ttl` to see the
   triples you wrote.

### Infer some more triples and validate your events

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

## Privacy policy

We do not collect, store, or share any personal data when you use these tools.

## Terms of service

This free, non-commercial project is provided “as is,” without
warranties of any kind. Use is at your sole risk; we disclaim all
liability for errors, omissions, or damages.
