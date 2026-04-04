export function sanitize(input: string): string {
  return input.trim().toLowerCase();
}

export function buildLabel(input: string): string {
  return `label:${sanitize(input)}`;
}
