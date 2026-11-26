# Troubleshooting by failure phase

| First failing phase | Investigate |
| --- | --- |
| Open or convert | Validate XML and encoding; resolve names and IDs; copy external resources; preserve the ALPX tree. Check the editor's active file and whether an older recovery copy was opened. |
| Compile | Start with the first error in Problems. Identify the Java field, callback, agent type, or generated declaration it refers to. Check local installed JAR signatures and imports. Correct the diagram or native model. Use generated sources to inspect ordering and signatures. |
| Start | Inspect initialization order, malformed wall geometry, level registration, selected elevator levels and empty geometry. Plain variable initialization ran before presentation markup was constructed in local generated 8.9.10 Java. Move dependent arrays into Main startup or resolve established markup references when needed. |
| Move | Confirm source, goal and current level belong together. Check collision geometry, door orientation and reachability. In the previous project, raw corner points written where a Wall expected anchor/control triples caused a startup exception. Compare the precise markup type with a local native artifact. |
| Board or unload | Confirm the selected car serves both endpoints, target differs from origin, and no wall or restricted region blocks its door. Check that each complete path has linked entry and exit ports. Distinguish waiting, inside-car and already-transported observations. |
| Stop or export | Confirm stop time, natural finish, output directory, counts and denominator. Check that the CSV timestamp is from the intended run. Stale CSV files and a prior successful build are weak evidence for a current model. |

**Observed locally.** Reproduced failures included obsolete elevator state symbols, invalid legacy Wall geometry, early reference initialization in generated code, and rejection of direct Java execution of a PLE-generated project. The installed JDK is useful for checking declarations and Java syntax. That is a distinct check from an AnyLogic experiment run.

If the project is open and its disk file changed, reload the updated file only after checking for unsaved changes. Verify one minimal route in the intended software before expanding scale, layout or modeling complexity. Keep the exact version, first error, project path, and outcome of each check.
