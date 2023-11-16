const std = @import("std");

const allocator = std.heap.page_allocator;

const http = std.http;
const json = std.json;
const fs = std.fs;
const base64 = std.base64;

const encoder = base64.standard.Encoder;

var client = http.Client{ .allocator = allocator };

const constants = @import("constants.zig");

const CLIENT_ID: []const u8 = constants.CLIENT_ID;
const CLIENT_SECRET: []const u8 = constants.CLIENT_SECRET;
const SPOTIFY_TOKEN_URL: []const u8 = "https://accounts.spotify.com/api/token";
const PLAYLIST_ID: []const u8 = constants.PLAYLIST_ID;
var ACCESS_TOKEN: []u8 = undefined;

const SpotifyTrack = struct {
    id: []const u8,
    name: []const u8,
};

const SpotifyTracks = struct {
    items: []SpotifyTrack,
};

const SpotifyPlaylist = struct {
    name: []const u8,
    tracks: SpotifyTracks,
};

const SongsResponse = struct {
    category_name: []u8,
    tracks: SpotifyTracks,
};

const AuthResponse = struct {
    access_token: []u8,
    token_type: []u8,
    expires_in: u64,
};

pub fn get_songs(comptime playlist_id: []const u8) !SongsResponse {
    var request = client.Request{
        .method = .GET,
        .uri = "https://api.spotify.com/v1/playlists/" ++ playlist_id,
        .headers = .{
            .{ "Authorization", "Bearer " ++ ACCESS_TOKEN },
        },
    };

    var response = try client.request(request);
    defer response.deinit();

    var body = try response.bodyStream().readAllAlloc(u8, std.heap.page_allocator);
    defer std.heap.page_allocator.free(body);

    return try json.parse(SpotifyPlaylist, body);
}

// pub fn download_song(prefix: []const u8, song_name: []const u8) !void {
//     var client = http.Client{};
//     var request = http.Request{
//         .method = .GET,
//         .url = "https://www.youtube.com/results?search_query=" ++ song_name,
//     };
//
//     var response = try client.request(request);
//     defer response.deinit();
//
//     var body = try response.bodyStream().readAllAlloc(u8, std.heap.page_allocator);
//     defer std.heap.page_allocator.free(body);
//
//     // Parse the response to get the YouTube video URL
//     var video_url = parse_video_url(body);
//
//     // Download the video using the YouTube API or any other library of your choice
//     // ...
//
//     // Save the downloaded song to a file
//     var file = try fs.cwd().createFile("songs/" ++ prefix ++ "_" ++ song_name ++ ".mp3");
//     defer file.close();
//
//     try file.writeAll(downloaded_song_data);
//
//     std.debug.print("Downloaded {}\n", .{song_name});
// }

fn get_access_token() !void {
    const auth_token: []const u8 = comptime CLIENT_ID ++ ":" ++ CLIENT_SECRET;
    var tmp: [((auth_token.len + 2) / 3) * 4]u8 = undefined;

    const auth_token_base64 = encoder.encode(&tmp, auth_token);

    // Concatenate: "Basic " + auth_token_base64
    const auth_token_base64_with_prefix = try std.fmt.allocPrint(allocator, "Basic {s}", .{auth_token_base64});
    defer allocator.free(auth_token_base64_with_prefix);

    const uri = try std.Uri.parse(SPOTIFY_TOKEN_URL);

    var headers = http.Headers{ .allocator = allocator };
    defer headers.deinit();
    try headers.append("Authorization", auth_token_base64_with_prefix);
    try headers.append("Content-Type", "application/x-www-form-urlencoded");

    var request = try client.request(.POST, uri, headers, .{});
    defer request.deinit();

    const body = "grant_type=client_credentials";

    request.transfer_encoding = .{ .content_length = 29 };

    try request.start(.{});

    try request.writer().writeAll(body);

    try request.finish();

    try request.wait();

    const response_body = request.reader().readAllAlloc(allocator, 8192) catch unreachable;
    defer allocator.free(response_body);

    const response = try json.parseFromSlice(AuthResponse, allocator, response_body, .{});

    ACCESS_TOKEN = response.value.access_token;
}

pub fn main() !void {
    try get_access_token();

    // var {playlist_name, songs} = try get_songs(playlist_id);
    // var songs = try get_songs(playlist_id);

    // for (songs.tracks) |song, idx| {
    //     try download_song(playlist_name, song.name);
    // / }
}
