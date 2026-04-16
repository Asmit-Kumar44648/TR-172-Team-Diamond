import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-sm border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-1 focus:ring-indigo-500/50 duration-200 ease-out",
  {
    variants: {
      variant: {
        default: "border-transparent bg-accent text-zinc-50 hover:bg-accent-hover",
        secondary: "border-transparent bg-surfaceElevated text-zinc-100 hover:bg-surfaceElevated/80",
        destructive: "border-transparent bg-danger text-zinc-50 hover:bg-danger/80",
        outline: "text-zinc-300 border-border",
        success: "border-transparent bg-success text-zinc-950",
        warning: "border-transparent bg-warning text-zinc-950",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }
