<!-- Improved compatibility of back to top link -->

<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!-- [![displayed text][displayed image url]][link url] -->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Enriquefft/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Information-Retrieval-BD2</h3>

<p align="center">
    Search and Information Retrieval system made for the DB2 course.
    <br />
    <a href="https://github.com/Enriquefft/Information-Retrieval-BD2/wiki"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

Information retrieval is the process of obtaining information from a collection
of documents.\
The goal of this project is to build a search engine that allows users to search
for songs. In the first part of the project, the search engine will be built
using the Single Pass In-Memory Indexing technique (SPIMI). The second part of
the project deals with data of multiple dimensions and the use of high
dimensional indexing techniques.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![FastAPI][FastAPI]][FastAPI-url]
- [![Flutter][Flutter]][Futter-url]
- [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
- [![AWS][AWS]][AWS-url]

### Dataset

The dataset contains over 18000 Spotify songs along with their lyrics and
information about the artist, genre, etc. The dataset is in CSV format and was
extrated from
[Kaggle](https://www.kaggle.com/imuhammad/audio-features-and-lyrics-of-spotify-songs).

Example of a document and attributes to be indexed:

```json
{
  "track_name": "Pangarap",
  "track_artist": "Barbie's Cradle",
  "lyrics": "Minsan pa Nang ako'y napalingon Hindi ko alam...",
  "playlist_genre": "rock",
  "playlist_subgenre": "classic rock"
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps, be aware
the index might take a while to build.

This project main development dependency is python-poetry, to install it follow
the instructions on the
[official documentation](https://python-poetry.org/docs/#installation)

### Prerequisites

```sh
poetry install
```

<!-- USAGE EXAMPLES -->

## Usage

<!-- poe the poet-->

The job runner [PoeThePoet](https://poethepoet.natn.io/) can be used to run the
different jobs of the project.

```sh
poe start # Starts the rest api server
```

```sh
poe clean # Removes the residual files from the previous index
```

```sh
poe db_init # Initializes the database and its indexes
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- OBJECTIVES -->

## Objectives

- [ ] Index documents in secondary memory through the construction of an
      Inverted Index using the Single Pass In-Memory Indexing technique.
  - Retrieve documents from the index using cosine similarity and the TF-IDF
    weighting scheme.

<!-- Sound -->

- [ ] Implement diferent inverse index for a multimedia collection of songs.

  - Extract the desired features for common use accros all methods
  - Implement an R-tree index for the embedding vectors of the songs.
  - Implement a high dimensional index using facebook's FAISS library.
  - Implement linear search using KNN.

- [ ] Emulate the functionality of song detection apps like Shazam.
  - Use a multimedia index to find the closest match to a given song.
  - Use a speech-to-text library to convert the song into text and then perform
    a text search using the documents inverse index.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MEMBERS -->

## Members

<table>
 <tr>
   <td>
     <img src="https://avatars.githubusercontent.com/u/102536323?s=400&v=4" alt="Aaron Camacho" width="200"/>
     <br/>
     <a href="https://github.com/AaronCS25">Aaron Camacho</a>
   </td>
   <td>
     <img src="https://avatars.githubusercontent.com/u/102196795?v=4" alt="Nicolas Castañeda" width="200"/>
     <br/>
     <a href="https://github.com/nicolas-castaneda">Nicolas Castañeda</a>
   </td>
   <td>
     <img src="https://avatars.githubusercontent.com/u/83974317?v=4" alt="Juaquín Remon" width="200"/>
     <br/>
     <a href="https://github.com/juaquin456">Juaquín Remon</a>
   </td>
   <td>
     <img src="https://avatars.githubusercontent.com/u/60308719?v=4" alt="Enrique Flores" width="200"/>
     <br/>
     <a href="https://github.com/Usuario_Autor_4">Enrique Flores</a>
   </td>
   <td>
     <img src="https://avatars.githubusercontent.com/u/83974266?s=400&u=f9e6664839a841ae781d3932ca156316ab35ea03&v=4" alt="Renato Cernades" width="200"/>
     <br/>
     <a href="https://github.com/RenatoCernades0107">Renato Cernades</a>
   </td>
 </tr>
</table>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png

<!-- Technologies -->

[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[Flutter]: https://img.shields.io/badge/Flutter-%2302569B.svg?style=for-the-badge&logo=Flutter&logoColor=white
[Futter-url]: https://flutter.dev/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[AWS]: https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white
[AWS-url]: https://aws.amazon.com/
