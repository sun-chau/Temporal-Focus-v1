            if (activeTasks.isEmpty()) {
                Box(
                    modifier = Modifier.weight(1f).fillMaxWidth(),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(24.dp))
                            .background(Color(0xFF161616))
                            .padding(vertical = 48.dp, horizontal = 24.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Info, // Use Info for now if PushPin is missing, let's try PushPin later. Actually, the user's image has a push pin. Let's stick with a generic icon or PushPin if we can.
                            contentDescription = null,
                            tint = Color.Gray,
                            modifier = Modifier.size(48.dp)
                        )
                        Spacer(Modifier.height(16.dp))
                        Text(
                            "No active chronometers ticking",
                            fontWeight = FontWeight.Bold,
                            color = Color.White,
                            fontSize = 18.sp
                        )
                        Spacer(Modifier.height(8.dp))
                        Text(
                            "Generate a target deadline timer to start mapping your urgency\nmilestones on the stage.",
                            color = Color.Gray,
                            fontSize = 14.sp,
                            textAlign = androidx.compose.ui.text.style.TextAlign.Center
                        )
                        Spacer(Modifier.height(24.dp))
                        Button(
                            onClick = { showCreateOverlay = true },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Color(0xFF252525),
                                contentColor = MaterialTheme.colorScheme.primary
                            )
                        ) {
                            Text("+ Create First Timer", fontWeight = FontWeight.Bold)
                        }
                    }
                }
            } else {
