# wav2bw64

This fork fixes the recent issue with an outdated FLASK version in 'setup.py'.  
It's now set as 'FLASK==2.1.0' (thanks to mfirth01 for finding out)  wb

A simple tool to add basic [ADM](https://adm.ebu.io/) metadata to a WAV file, according to [EBU Production Profile](https://tech.ebu.ch/publications/adm-production-profile) and export it as [BW64](https://www.itu.int/rec/R-REC-BS.2088/en) file.

<img width="1483" alt="adm_authoring_v0 1 0-alpha2" src="https://user-images.githubusercontent.com/5551263/111299250-038cd900-8650-11eb-896c-f2ed73575a41.png">

## Installation

```bash
pip install .
```

## Usage

### Command Line Usage

```bash
wav2bw64 infile.wav outfilebw64.wav adm.yaml
```

### Web GUI Usage

Start Web server:

```bash
adm_author --host 127.0.0.1 --port 8080 
```

Open http://127.0.0.1:8080 in your Browser 

### ADM config in YAML file

Basic example structure:

```yaml
- name: Audio Programme 1
  language: eng
  loudness: -23
  apItems:
  - name: Stereo Bed
    routing: [1, 2]
    type: 0+2+0
  - name: English Dialogue
    routing: [4]
    type: Object
    object_parameter:
      position: {azimuth: 0, distance: 1, elevation: 14}
    importance: 10
    interactivity:
      onOffInteract: false
      azRange: [-30, 30]
      elRange: [-30, 30]
      positionInteract: true
- name: Audio Programme 2
  language: ger
  loudness: -23
  apItems:
  - name: Stereo Bed
    routing: [1, 2]
    type: 0+2+0
    importance: 10
    interactivity:
      onOffInteract: false
      azRange: [-30, 30]
      elRange: [-30, 30]
      gainInteract: false
      gainInteractionRange: [-6, 6]
      positionInteract: false
  - name: German Dialogue
    routing: [3]
    type: Object
    importance: 10
    object_parameter:
      position: {azimuth: 0, distance: 1, elevation: 0}
```

This configures two audioProgrammes, one with the name "Audio Programme 1" and one with "Audio Programme 2". The first audioProgramme contains two audioObjects, one with an Object type and one with 0+2+0 DirectSpeakers type. The routing array defines the track indices for the CHNA chunk. It is possible to refer to the same track indices multiple times, as it is done in the example.


## GUI Usage

The web-based authoring tool enables users to upload a WAV file (axml chunks are curently ignored) and to add ADM Metadata to it such as
- AudioProgrammes 
- language of Audio Programmes
- Items (DirectSpeaker & Object) for Audio Programmes depending on uploaded wav file channel count
- Routing to wav file track indices for items
- Interactivity options
- Importance options
- Object settings

The metadata can be generated by exporting the ADM structure. That will be saved in an axml chunk which is attached to a copy of the uploaded wav file, so basically a new BW64 file.


## GUI Development

In production mode, the Flask server is just using a bundled Javascript and CSS which was generated using [Svelte](https://svelte.dev/). To change the bundeled Javascript and CSS, the Svelte project needs to be build again: 

### Dependencies installation

```bash
cd svelte_app
npm install
```

### Environments
Using 

```bash
npm run build
```

will just build the Svelte project once and close, whilst

```bash
npm run dev
```

will start a webserver (which is actually not needed, since we are using Flask as webserver) in development mode which will rebuild the bundles on every change.
