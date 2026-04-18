export type Hex = `0x${string}`

export interface ManifestAttestation {
  seedId: Hex
  manifestHash: Hex
  ciphertextHash: Hex
  termId: bigint
  deadline: bigint
}

export interface DecryptionAttestation {
  requestId: Hex
  seedId: Hex
  plaintextHash: Hex
  completionHash: Hex
  termId: bigint
  deadline: bigint
}

export interface ThresholdBindingProfile {
  profileId: Hex
  provider: "lit" | "taco"
  networkName: string
  threshold: number
  committeeSize: number
  timeoutSeconds: number
  policyHash: Hex
}
