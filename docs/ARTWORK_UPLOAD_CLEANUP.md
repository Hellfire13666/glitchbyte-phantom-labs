# Archived artwork upload housekeeping

This is a provenance log for a cleanup of temporary nested upload-kit folders. Tool images on canonical paths `artwork/tool-covers/<number>_<tool>.png` are preserved, and the map `docs/TOOL_COVER_MAP.json` remains authoritative.

All 30 duplicate PNG bytes were checked against an existing official cover's Git object SHA before removal. Four associated temporary upload-kit notes/manifests were removed from the tool-cover upload area to keep it tidy. No tool source files or official cover assets were deleted.

This log preserves the former tracked paths and blob SHAs if historical recovery is needed through Git history.

| Former path | Git blob SHA |
|---|---|
| `artwork/tool-covers/approved_four_covers_upload/06_ip_specter.png` | `73fc6421d1d11c20dc791f70578e24e63d4e4746` |
| `artwork/tool-covers/approved_four_covers_upload/10_velvetecho.png` | `373bb917781a3bc2c4c355fc69ff42bd6e46a3a1` |
| `artwork/tool-covers/approved_four_covers_upload/15_screamframe.png` | `9d5909f5b32b5eb6ac41533d92fd13abcb25a277` |
| `artwork/tool-covers/approved_four_covers_upload/16_ghostmark.png` | `61b98865df1939cc97cc5a403b46b5d0bb14cbaf` |
| `artwork/tool-covers/phantom_labs_named_artwork_upload_kit/ARTWORK_MANIFEST.json` | `44dab562f11232c34bca7b14fce11ec30aed059d` |
| `artwork/tool-covers/phantom_labs_named_artwork_upload_kit/README_FIRST.md` | `61aa1eb4c24bf19ad38732dbf6f3428ce7224c0c` |
| `artwork/tool-covers/phantom_labs_named_artwork_upload_kit/artwork/tool-covers/05_neon_rose_phantom_3.png` | `146106d2e848df6c8219f824fd0db40b1e15fb10` |
| `artwork/tool-covers/phantom_labs_named_artwork_upload_kit/artwork/tool-covers/08_voidlantern.png` | `6823eb62922b13c6433309f54d7250778b5c45ca` |
| `artwork/tool-covers/phantom_labs_named_artwork_upload_kit/artwork/tool-covers/09_username_intel.png` | `58fa6bfb91f0fbc0f2ad88470fdc3d449b98d33b` |
| `artwork/tool-covers/phantom_labs_named_artwork_upload_kit/artwork/tool-covers/12_x_intel_phantom.png` | `7086b8b78a7145ac11dcc4fad922804c2d7c491d` |
| `artwork/tool-covers/phantom_labs_named_artwork_upload_kit/artwork/tool-covers/13_x_shadow_no_api.png` | `9752e7f6608516e468852314a8c03bc19c5b78fe` |
| `artwork/tool-covers/phantom_labs_named_artwork_upload_kit/artwork/tool-covers/17_log_constellation.png` | `d7de7800783f4d268ab5d8c990cd50b56e94b27b` |
| `artwork/tool-covers/phantom_labs_named_artwork_upload_kit/artwork/tool-covers/19_hexwake.png` | `2ef5f742193bd31d9d739ef9a1c765d61a7650d6` |
| `artwork/tool-covers/phantom_labs_named_artwork_upload_kit/artwork/tool-covers/20_phantom_cipherbox.png` | `2b5f578c2d7e43d4509f8b15cd32ff29897d7340` |
| `artwork/tool-covers/phantom_labs_named_artwork_upload_kit/artwork/tool-covers/21_catch_me_in_the_chaos.png` | `254ff2073d5c7966fa1b46b18a6c69f460dbea89` |
| `artwork/tool-covers/phantom_labs_named_artwork_upload_kit/artwork/tool-covers/23_ghost_in_my_heart.png` | `66174d98b9b1085baf2ffe828f17ec5b6569549d` |
| `artwork/tool-covers/phantom_labs_named_artwork_upload_kit/artwork/tool-covers/24_find_me_if_you_love_me.png` | `588cbf97acaac34fff9a902c27df069ddb43c1e3` |
| `artwork/tool-covers/phantom_selected_publish_bundle/README_FIRST.md` | `b876ad59d4141b7799fea05c52ed876bb59c7892` |
| `artwork/tool-covers/phantom_selected_publish_bundle/SELECTED_MANIFEST.json` | `bae889e90dab5d8b50ee53cbfee117f175a01f60` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/03_domain_intel.png` | `d54210601c9e8b7382f50b2650ea0669d1d89915` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/04_domain_phantom.png` | `f985a2254d2973504fdb248ac168ddcd1479aa3b` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/05_neon_rose_phantom_3.png` | `146106d2e848df6c8219f824fd0db40b1e15fb10` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/08_voidlantern.png` | `6823eb62922b13c6433309f54d7250778b5c45ca` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/09_username_intel.png` | `58fa6bfb91f0fbc0f2ad88470fdc3d449b98d33b` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/11_rose_crawler.png` | `386978b0dc26158ea8eec70a0ce0f6faa9ace529` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/12_x_intel_phantom.png` | `7086b8b78a7145ac11dcc4fad922804c2d7c491d` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/13_x_shadow_no_api.png` | `9752e7f6608516e468852314a8c03bc19c5b78fe` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/17_log_constellation.png` | `d7de7800783f4d268ab5d8c990cd50b56e94b27b` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/19_hexwake.png` | `2ef5f742193bd31d9d739ef9a1c765d61a7650d6` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/20_phantom_cipherbox.png` | `2b5f578c2d7e43d4509f8b15cd32ff29897d7340` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/21_catch_me_in_the_chaos.png` | `254ff2073d5c7966fa1b46b18a6c69f460dbea89` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/22_dark_desire.png` | `08623891b2e7bf9c326807923ea873b7c4b181e7` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/23_ghost_in_my_heart.png` | `66174d98b9b1085baf2ffe828f17ec5b6569549d` |
| `artwork/tool-covers/phantom_selected_publish_bundle/artwork/tool-covers/24_find_me_if_you_love_me.png` | `588cbf97acaac34fff9a902c27df069ddb43c1e3` |

**Recovery**: Earlier Git commits retain all former blobs. Refer to repository history rather than putting nested duplicates back into the live tool-cover area.
